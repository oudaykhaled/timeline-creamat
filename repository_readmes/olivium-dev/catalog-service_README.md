# README for olivium-dev/catalog-service

# Catalog-Service Documentation

#### Introduction:
Catalog-Service is a RESTful API that provides CRUD operations. Users can create, read, update, and delete Item(s), add and remove tags, search, and build an hierarchical structure.

#### Properties:
An Item has the following properties:

- ID (unique identifier)
- ParentID (the ID of the parent item, null if there is no parent)
- Type (e.g., song, image, audiobook, SKU, etc.)
- Name (textual description of the item)
- Description (textual description of the item)
- Tags (an array of tags)
- CreatedAt (timestamp when the item was created)
- UpdatedAt (timestamp when the item was last updated)

#### Apis:

##### Item:
POST /item: Create a new item with the following properties:

- Parent (the ID of the parent item, null if there is no parent)
- Type (e.g., song, image, audiobook, SKU, etc.)
- Tags (an array of tags)
- Name (textual description of the item)
- Description (textual description of the item)

PUT /item: Update an existing item with the following properties:

- ID (unique identifier)
- Parent (the ID of the parent item, null if there is no parent)
- Type (e.g., song, image, audiobook, SKU, etc.)
- Name (textual description of the item)
- Description (textual description of the item)

POST /item/search: Search item(s) with the following properties:

- Query (textual name of description)
- Type (e.g., song, image, audiobook, SKU, etc.)
- Tags (an array of tags)
- PageSize (the number of results that are returned in a single page)
- PageNumber (indicates which page of results should be returned)

POST /item/tag/add: Add tag(s) to an existing item with the following properties:

- ID (unique identifier)
- Tags (an array of tags)

POST /item/tag/remove: Remove tag(s) to an existing item with the following properties:

- ID (unique identifier)
- Tags (an array of tags)

GET /item/{ID}: Retrieve an existing item by unique identifier

DEL /item/{ID}: Delete an existing item by unique identifier

##### Category:
POST /category: Create a new category with the following properties:

- Name (textual description of the category)

PUT /category: Update an existing category with the following properties:

- ID (unique identifier)
- Name (textual description of the category)

GET /category/{ID}: Retrieve an existing category by unique identifier

GET /category/all/{pageSize}/{pageNumber}: Retrieve categories by page size and page number

DEL /category/{ID}: Delete an existing category by unique identifier
