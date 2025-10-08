from rest_framework import generics
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .serializers import ChatMessageSerializer, ChatInputSerializer, ChatSessionSerializer
from .graph import get_graph
from langchain_core.messages import HumanMessage, AIMessage

class ChatView(generics.GenericAPIView):
    serializer_class = ChatInputSerializer

    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        message_text = request.data.get('message')

        session = None
        if session_id:
            try:
                session = ChatSession.objects.get(pk=session_id)
            except ChatSession.DoesNotExist:
                pass # If session_id is provided but doesn't exist, a new session will be created below

        if not session:
            session = ChatSession.objects.create()

        # Save user message
        ChatMessage.objects.create(session=session, message=message_text, is_user=True)

        # Get chat history
        history = session.messages.all().order_by('created_at')
        messages = [HumanMessage(content=msg.message) if msg.is_user else AIMessage(content=msg.message) for msg in history]

        graph = get_graph()
        full_ai_response_chunks = []
        for chunk in graph.stream({"messages": messages}):
            if "__end__" in chunk:
                break
            if "chatbot" in chunk:
                for message in chunk["chatbot"]["messages"]:
                    content_to_yield = ""
                    if hasattr(message, "content"):
                        content_to_yield = message.content
                    elif isinstance(message, dict) and "content" in message:
                        content_to_yield = message["content"]
                    
                    if content_to_yield:
                        full_ai_response_chunks.append(content_to_yield)
        
        # Save AI message
        final_ai_response = "".join(full_ai_response_chunks)
        ChatMessage.objects.create(session=session, message=final_ai_response, is_user=False)

        return Response({
            'session_id': session.pk,
            'response': final_ai_response
        })

class SessionMessageView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        session_id = self.kwargs['id']
        return ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
