
# Available Time Router
available_time_router = APIRouter(prefix="/available-times", tags=["Available Times"])

@available_time_router.get("/skill/{skill_id}")
async def get_available_times_by_skill(
    skill_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    available_time_service = SkillAvailableTimeService(db)
    return await available_time_service.get_available_times_by_skill(skill_id)

@available_time_router.get("/day/{day}")
async def get_available_times_by_day(
    day: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    available_time_service = SkillAvailableTimeService(db)
    return await available_time_service.get_available_times_by_day(day)

@available_time_router.post("/")
async def add_available_time(
    time_data: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    available_time_service = SkillAvailableTimeService(db)
    return await available_time_service.add_available_time(time_data)

@available_time_router.put("/{time_id}")
async def update_available_time(
    time_id: str,
    time_data: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    available_time_service = SkillAvailableTimeService(db)
    return await available_time_service.update_available_time(time_id, time_data)

@available_time_router.delete("/{time_id}")
async def soft_delete_available_time(
    time_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    available_time_service = SkillAvailableTimeService(db)
    return await available_time_service.soft_delete_available_time(time_id)
