from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(25),nullable=False, unique=True)
    firstName: Mapped[str] = mapped_column(String(20),nullable=False)
    lastName: Mapped[str] = mapped_column(String(30),nullable=False) 

    posts: Mapped[list["Post"]] = relationship(back_populates = "user")
    comments: Mapped[list["Comment"]] = relationship(back_populates = "user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    user: Mapped[list["User"]] = relationship(back_populates ="posts")
    media: Mapped[list["Media"]] = relationship(back_populates = "post")
    comments: Mapped[list["Comment"]] = relationship(back_populates = "post")


    
    def serialize(self): 
        return {
            "id_user": self.id_user
        }
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)

    post: Mapped[list["Post"]] = relationship(back_populates = "media")
     
    def serialize(self):
        return {
            "url": self.url,
            "type": self.type
        }
    
class Comment(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    post: Mapped[list["Post"]] = relationship(back_populates = "comments")
    user: Mapped[list["User"]] = relationship(back_populates = "comments")

    def serialize(self) :
        return {
            "text": self.text,
            "user_id": self.user_id,

        }
    
class Followers(db.Model):

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int]= mapped_column(ForeignKey("user.id"), primary_key=True)
    
    follower = relationship("User", foreign_keys = [user_from_id], backref="following")
    followed = relationship("User", foreign_keys = [user_to_id], backref="followers")

    def serialize(self) :
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
    






