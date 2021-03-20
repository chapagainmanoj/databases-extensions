from _pytest.mark import param
import pytest
from sqlalchemy.dialects import sqlite
from sqlalchemy.schema import CreateTable, DropTable
from sqlalchemy.sql.expression import column, select
from extensions import CursorPagination, PaginationParams, SearchType
from sqlalchemy.sql import text

PAGE_PARAMS = PaginationParams.construct(first=3)
SEARCH_PARAMS = PaginationParams.construct(
    first=3, search=SearchType.construct(columns=["text"], value="2")
)
FILTER_PARAMS = PaginationParams.construct(
    first=3, filter={"completed.is_true": ""}
)


async def drop_db(database, query):
    await database.execute(query=query)
    await database.disconnect()


@pytest.mark.asyncio
async def test_pagination(database, notes, notes_data):
    await database.connect()

    # Create table
    dialect = sqlite.dialect()
    create_query = str(CreateTable(notes).compile(dialect=dialect))
    await database.execute(query=create_query)

    # Insert
    query = notes.insert()
    await database.execute_many(query=query, values=notes_data)

    # Fetch multiple rows
    query = notes.select()
    pagination = CursorPagination(database, query)
    paginated = await pagination.page(PAGE_PARAMS)
    assert len(paginated.edges) == PAGE_PARAMS.first
    assert paginated.page_info.has_next_page == True
    assert paginated.page_info.has_previous_page == False

    searched = await pagination.page(SEARCH_PARAMS)
    assert len(searched.edges) == 1

    filtered = await pagination.page(FILTER_PARAMS)
    actual = [e.node["completed"] for e in filtered.edges]
    expected = [True] * FILTER_PARAMS.first
    assert actual == expected

    drop_query = str(DropTable(notes).compile(dialect=dialect))
    await drop_db(database, drop_query)
