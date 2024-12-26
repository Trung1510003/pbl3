from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, password={self.password}, username={self.username}, email={self.email})>"

class Conversation(Base):
    __tablename__ = 'Conversations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title={self.title}, user_id={self.user_id})>"

class Message(Base):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('Conversations.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    sender = Column(Enum('user', 'chatbot'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, sender={self.sender}, conversation_id={self.conversation_id})>"

username = "root"
password = "admin"
DATABASE_URL = f"mysql+pymysql://{username}:{password}@localhost/chat52hz"  # Cập nhật thông tin kết nối
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def add_user(username, password, email=None):
    new_user = User(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    return new_user

def get_user(username):
    return session.query(User).filter(User.username == username).first()

def add_conversation(user_id, title):
    new_conversation = Conversation(user_id=user_id, title=title)
    session.add(new_conversation)
    session.commit()
    return new_conversation

def get_conversations_by_user(user_id):
    return session.query(Conversation).filter(Conversation.user_id == user_id).all()

def add_message(conversation_id, message, sender):
    new_message = Message(conversation_id=conversation_id, message=message, sender=sender)
    session.add(new_message)
    session.commit()
    return new_message

def get_messages_by_conversation(conversation_id):
    return session.query(Message).filter(Message.conversation_id == conversation_id).all()


