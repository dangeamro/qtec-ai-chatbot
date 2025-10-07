from rest_framework import generics
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .models import ChatSession, ChatMessage
from .serializers import ChatMessageSerializer
from .graph import get_graph
from langchain_core.messages import HumanMessage, AIMessage

class ChatView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        message_text = request.data.get('message')

        if session_id:
            session = ChatSession.objects.get(pk=session_id)
        else:
            session = ChatSession.objects.create()

        # Save user message
        ChatMessage.objects.create(session=session, message=message_text, is_user=True)

        # Get chat history
        history = session.messages.all().order_by('created_at')
        messages = [HumanMessage(content=msg.message) if msg.is_user else AIMessage(content=msg.message) for msg in history]

        def stream_response():
            graph = get_graph()
            ai_response = ""
            for chunk in graph.stream({"messages": messages}):
                if "messages" in chunk:
                    for message in chunk["messages"]:
                        ai_response += message.content
                        yield message.content
            
            # Save AI message
            ChatMessage.objects.create(session=session, message=ai_response, is_user=False)

        return StreamingHttpResponse(stream_response())

class SessionMessageView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        session_id = self.kwargs['id']
        return ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
