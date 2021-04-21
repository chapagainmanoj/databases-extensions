# databases-query-extensions
An query building extensions for sqlalchey with encode/databases to apply pagination, filter, search and sorting to query

## Installation

```pip install databases-extensions```

## Example
Construct page params
  ```python
  page_params = PaginationParams.construct(
        first=3, filter={"completed.is_true": ""}
    )
  ```
apply cursor pagination and get results
  ```python
    from extensions import CursorPagination
    ...
    query = example.select()
    pagination = CursorPagination(database, query)
    paginated = await pagination.page(page_params)
  ```

apply filters, search, sorting or pagination and get query 

```
    from extensions import query_builder
    ...
    query = example.select()
    cursor_column="created_date"
    query = query_builder(query, page_params, cursor_column)
```

  A complete query params example
```python
{
    "first": 100,
    "after": <cursor>,
    "afterWith": <cursor>,
    "search": {
      "columns": ["col1", "col2"],
      "value": "new"
    },
    "filter": {
      "status.eq": "Pending"
    },
    "sort": "createdAt",
    "order": "asc"
  }
  ```
