
class ReviewModel(BaseModelClass):
    __tablename__ = "REVIEWS"

    reviewer_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    reviewee_id: Mapped[str] = mapped_column(ForeignKey("USER.id"))
    skill_share_id: Mapped[str] = mapped_column(ForeignKey("SKILL_SHARE_REQUESTS.id"))
    rating = mapped_column(Enum(ReviewRatingEnum))
    comment = mapped_column(Text, nullable=True)

    # Relationships
    reviewer = relationship("UserModel", foreign_keys=[reviewer_id])
    reviewee = relationship("UserModel", foreign_keys=[reviewee_id])


    skill_share = relationship("SkillShareRequestModel", back_populates="reviews")
