import datetime
from typing import Any

from sqlalchemy import extract, func, select

from app.config.database.db import session_manager
from app.core.stats.types import WeeklyReport


# Define your async engine and session
# Helper function to get the day name from its number (1 = Monday, 2 = Tuesday, etc.)
def get_day_name(day_number: int) -> str:
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day_number - 1] if 1 <= day_number <= 7 else 'Unknown'


async def convert_stats_to_list(stats: dict[str, int]) -> list[WeeklyReport]:

    weekly_reports: list[WeeklyReport] = []
    for day, count in stats.items():
        weekly_reports.append(WeeklyReport(name=day, value=count))

    return weekly_reports

async def get_daily_stats(model: Any, other_matches: dict[str, Any]|None = None) -> list[WeeklyReport]:
    async with session_manager.session() as session:
        try:
            # Define the date range
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=7)

            # Build the query
            query = (
                select(
                    extract('dow', model.created_at).label('day'),
                    func.count().label('stats')
                )
                .filter(model.created_at >= start_date, model.created_at < end_date)
            )

            # Apply additional filters if any
            if other_matches:
                for key, value in other_matches.items():
                    query = query.filter(getattr(model, key) == value)

            # Group by day of week
            query = query.group_by('day').order_by('day')

            result = await session.execute(query)
            stats = result.fetchall()

            formatted_stats = {get_day_name(row.day + 1): row.stats for row in stats}

            data= await convert_stats_to_list(formatted_stats)
            return data
        except Exception as e:
            
            print(f"Error getting daily stats: {e}")
            raise

