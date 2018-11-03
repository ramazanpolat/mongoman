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
    
    # You can use ORM Prodict
    
    class Customer(Prodict):
        name: str
        age: int

        def __repr__(self):
            return 'Customer(name=%s, age=%d)' % (self.name, self.age)
            
        @property
        def number(self):
            return 42
            
            
    customers = mm.collection('customers')
    
    # Add 'model' parameter to map the result to a Prodict object
    customer = customers.find_one(model=Customer)
    print(customer)
    print('name:', customer.name) 
    print('age:', customer.age)
    print('type:', type(customer).__name__)
        
    # Customer(name=tango, age=42)
    # name: tango
    # age: 42
    # type: Customer
```
    
    
        

