## Product Service

#### Create a Product

```
POST /product
```

##### Parameters - `Parameter`

| Name      | Type     | Description                                             |
| --------- | -------- | ------------------------------------------------------- |
| name      | `string` | **required** <p>name of the product</p>                 |
| price     | `number` | **required** <p>price of the product</p>                |
| userId    | `number` | **required** <p>id of the user creating the product</p> |
| ShortDesc | `string` | **optional** <p>short description of the product</p>    |

#### Get List of Products

```
GET /products
```

#### Get a Product

```
GET /product/:productId
```

#### Update a Product

```
PUT /product/:productId
```

##### Parameters - `Parameter`

| Name      | Type     | Description                                          |
| --------- | -------- | ---------------------------------------------------- |
| name      | `string` | **optional** <p>name of the product</p>              |
| price     | `number` | **optional** <p>price of the product</p>             |
| ShortDesc | `string` | **optional** <p>short description of the product</p> |

#### Delete a Product

```
DELETE /product/:productId
```

## Order Service

#### Create an Order

```
POST /order
```

##### Parameters - `Parameter`

| Name    | Type            | Description                                                         |
| ------- | --------------- | ------------------------------------------------------------------- |
| User    | `number`        | **required** <p>user to whom the order belongs to</p>               |
| Product | `Array<number>` | **required** <p>List of the product ids in the order</p>            |
| Address | `string`        | **required** <p>users address where the order should be shipped</p> |

#### Get List of Orders

```
GET /order
```

#### Get an Order

```
GET /order/:orderId
```

#### Update an order

```
PATCH /order/:orderId/address
PATCH /order/:orderId/product
PATCH /order/:orderId/status
```

##### Parameters - `Parameter`

| Name    | Type            | Description                                                            |
| ------- | --------------- | ---------------------------------------------------------------------- |
| Address | `string`        | **required** <p>users address where the order should be shipped</p>    |
| Product | `Array<number>` | **required** <p>List of the product ids in the order</p>               |
| Status  | `enum`          | **required** <p>`ORDER_PLACED` `ORDER_ON_ROUTE` `ORDER_DELIVERED` </p> |

#### Delete an Order

```
DELETE /order/:orderId
```

### Order Service Event Consumers

#### Consume `Product.Created` event from product service

```
POST /consume/product/created
```

##### Parameters - `Parameter`

| Name      | Type       | Description                                             |
| --------- | ---------- | ------------------------------------------------------- |
| Id        | `string`   | **required** <p>id of the product</p>                   |
| Name      | `string`   | **required** <p>name of the product</p>                 |
| UserId    | `number`   | **required** <p>id of the user creating the product</p> |
| Price     | `number`   | **required** <p>price of the product</p>                |
| ShortDesc | `string`   | **optional** <p>short description of the product</p>    |
| CreatedAt | `datetime` | **optional** <p>product created date</p>                |
| UpdatedAt | `datetime` | **optional** <p>product updated date</p>                |

#### Consume `Product.Updated` event from product service

```
POST /consume/product/updated
```

##### Parameters - `Parameter`

| Name      | Type       | Description                                             |
| --------- | ---------- | ------------------------------------------------------- |
| Id        | `string`   | **required** <p>id of the product</p>                   |
| Name      | `string`   | **required** <p>name of the product</p>                 |
| UserId    | `number`   | **required** <p>id of the user creating the product</p> |
| Price     | `number`   | **required** <p>price of the product</p>                |
| ShortDesc | `string`   | **optional** <p>short description of the product</p>    |
| CreatedAt | `datetime` | **optional** <p>product created date</p>                |
| UpdatedAt | `datetime` | **optional** <p>product updated date</p>                |

#### Consume `Product.Deleted` event from product service

```
POST /consume/product/deleted
```

##### Parameters - `Parameter`

| Name      | Type       | Description                                             |
| --------- | ---------- | ------------------------------------------------------- |
| Id        | `string`   | **required** <p>id of the product</p>                   |
| Name      | `string`   | **required** <p>name of the product</p>                 |
| UserId    | `number`   | **required** <p>id of the user creating the product</p> |
| Price     | `number`   | **required** <p>price of the product</p>                |
| ShortDesc | `string`   | **optional** <p>short description of the product</p>    |
| CreatedAt | `datetime` | **optional** <p>product created date</p>                |
| UpdatedAt | `datetime` | **optional** <p>product updated date</p>                |
