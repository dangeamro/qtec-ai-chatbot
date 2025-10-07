from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from .graph import get_graph
from langchain_core.messages import HumanMessage

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session = self.get_object()
        message_text = request.data.get('message')

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

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        session = ChatSession.objects.get(pk=pk)
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
