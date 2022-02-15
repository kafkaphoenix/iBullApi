# iBull Stock Trades

iBull is a social trading brokerage company that focuses on providing financial and copy trading services for anyone
 without much experience on it.
 
They have to develop a new API to allow them to manage a collection of stock trades of their users. They have
 a huge number of transactions and their team cannot be in charge of developing this API.
 
## Requirements

The API has the following endpoints:

* `POST /trades` handles the creation of a new trade
* `GET /trades` returns a collection of all trades
* `GET /trades/<id>` returns a trade with the given id
* `DELETE /trades/<id>` removes a trade with the given id

The company has also defined how should be the Trade JSON object. Here you could see an example: 

```json
{
    "id": 1,
    "type": "buy",
    "user_id": 23,
    "symbol": "ABX",
    "shares": 30,
    "price": 134,
    "timestamp": 1531522701000
}
```

### Constraints

Due to the business logic of their business, here you could find a list of constraints for each
 endpoint of the API. 
 
* `POST /trades`
    * Expects a JSON Trade object **without** an id property as a body payload. 
    * If the shares value is out of the accepted range [1, 100], 
    or the type value is invalid (i.e., not 'buy' or 'sell'), the API must return error code 400. 
    * As the trades has no id, you have to create and assign one. To do so, use an autoincrement id, starting at 1.
    * If everything goes right, the response code is 201, and the response body is the created trade object.
    
* `GET /trades`
    * Optionally accepts query parameters `type` and `user_id`, for example `/trades/?type=buy&user_id=122`. 
    All these parameters are optional. In case they are present, only objects matching the parameters must be returned.
    * The response code is 200, and the response body is an array of all trade objects ordered by their 
    ids in increasing order.
    
* `GET /trades/<id>`
    * If the matching trade exists, the response code is 200 and the response body is the matching trade object.
    * If there is no trade with the given id in the collection, the response code is 404.

* `DELETE /trades/<id>`
    * If the matching trade exists, the response code is 204.
    * If there is no trade with the given id in the collection, the response code is 404.
    

## What are we looking for?

* **Put all tests in green**. Implement the previous requirements, in order to make tests pass. Feel free to 
use any dependency or service to improve your solution.

* **A well-designed solution and architecture**. Avoid duplication, extract re-usable code
where makes sense. We want to see that you can create an easy-to-maintain codebase.

* **Test as much as you can**. One of the main pain points of maintaining other's code
comes when it does not have tests. So try to create tests covering, at least, the main classes.