from sqlalchemy import ForeignKey, Text, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dao.database import Base


class Blog(Base):
    __tablename__ = "blogs"

    title: Mapped[str]
    author: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    short_description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(default="published", server_default="published")
    user: Mapped["User"] = relationship("User", back_populates="blogs")
    blogs: Mapped[list["Blog"]] = relationship(back_populates="user")

    # Связь с тегами через промежуточную таблицу
    tags: Mapped[list["Tag"]] = relationship(
        secondary="blog_tags", back_populates="blogs"
    )


class Tag(Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(50), unique=True)

    # Обратная связь с блогами
    blogs: Mapped[list["Blog"]] = relationship(
        secondary="blog_tags", back_populates="tags"
    )


class BlogTag(Base):
    __tablename__ = "blog_tags"

    blog_id: Mapped[int] = mapped_column(
        ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    )

    # Уникальное ограничение для предотвращения дублирования
    __table_args__ = (UniqueConstraint("blog_id", "tag_id", name="uq_blog_tag"),)
    # Уникальное ограничение UniqueConstraint('blog_id', 'tag_id') гарантирует, что мы не сможем случайно добавить один и тот же тег к одному блогу дважды.
