# mongoman
PyMongo wrapper that provides ORM and easy MongoDB connection handling.


# features

Opening and closing MongoDB connection in all over your code is not a good practice.

MongoMan provides a default instance which you can use in anywhere in your code to access to MongoDB, without needing to connect it again.

main.py
```python
    from mongoman import MongoMan
    
    mm = MongoMan(host='localhost', port=27017, user='username', password='password')

    customers = mm.collection('customers')

    for customer in customers.find():
        print(customer)

    # {_id:'5bdca8840ab05daa3f2f1e72', name:'John Appleseed', age:42}
    # {_id:'5bdca8840ab05daa3f2f1e84', name:'Middle Man', age:38}
```

side.py

```python
    # --- IN SOME OTHER FILE ---
    from mongoman import MongoMan
    
    # if you are already connected to MongoDB in somewhere else, just get the default instance
    mm = MongoMan.default_instance()
    
    customers = mm.collection('customers')
    
    # Add 'model' parameter to map the result to a Prodict object
    customer = customers.find_one(model=Prodict)
    print(customer)
    print('name:', customer.name) 
    print('age:', customer.age)
    print('type:', type(customer).__name__)
        
    # {'_id':'5bdca8840ab05daa3f2f1e72', 'name'=tango, 'age'=42]
    # name: tango
    # age: 42
    # type: Prodict
```

if you want to have auto code completion for mapped [Prodict](https://github.com/ramazanpolat/prodict) objects(they are essentially ``dict`` objects supporting dot-accessible attributes), you can define a model beforehand like this:

```python
    
    class Customer(Prodict):
        name: str
        age: int
        
    customers = mm.collection('customers')
    
    # Add 'model' parameter to map the result to a Prodict object
    customer = customers.find_one(model=Customer)
    print(customer)
    print('name:', customer.name) 
    print('age:', customer.age)
    print('type:', type(customer).__name__)
    
    # {'_id':'5bdca8840ab05daa3f2f1e72', 'name'=tango, 'age'=42]
    # name: tango
    # age: 42
    # type: Customer
````
Prodict models are pretty straightforward but you can check repo of [Prodict](https://github.com/ramazanpolat/prodict) in order to get more info.

        

# Thanks
I would like to thank to [JetBrains](https://www.jetbrains.com/) for creating [PyCharm](https://www.jetbrains.com/pycharm/), the IDE that made my life better.

