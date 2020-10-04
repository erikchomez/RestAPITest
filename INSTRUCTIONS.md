# Simple API

## Instructions
The goal for this assignment is to create a simple REST API around the data
for a set of 50k products.

To complete the assignment, implement one or more of the endpoints below
in a lightweight standalone service. You are welcome to use Node.JS,
Python, Java, Scala, C#, or Go and you may use helper frameworks for the
REST API support (ie, Express, Flask, Dropwizard, Spring Boot, Kestrel,
mux, etc). Do not use external applications or dependencies (like a
database), and avoid or minimize the use of external libraries (ie
collections.js or guava). If you can, demonstrate that you know how to
accomplish what those libraries would do for you by implementing it in a
language-native way (you can explain in your documentation what you would
use normally).

Provide a Dockerfile that we can build and execute, or instructions on
how to build and execute your service. It should run at
http://localhost:8088.

Include a SOLUTION.md file that describes your design and
implementation decisions with time and memory analysis for your
implementation (ie, big O). Ideal solutions should be able to provide
results quickly and efficiently regardless of the size of the product set
while minimizing the footprint of the service.

We are looking for:
- a working solution
- clean code
- optimized search operations
- data modeling and design
- error handling
- solution description
- memory and runtime analysis
- time to completion

We think it should take less than 4 hours to produce a typical solution.
When you are done, zip up the code and the SOLUTION.md file and send it to us by email.

### Endpoint #1
#### POST /api/products/autocomplete
Implement an autocomplete endpoint that can provide suggestions for product
name, category, and brand given a prefix.

Request example:

    { "type": "brand", "prefix": "Can" }

Response example:

    ["Canon","Candyoo","Canless Air System","Cangshan","Canyon Dancer","Cannon Safe","Canonet","CandyHome","Canopy"]

### Endpoint #2
#### POST /api/products/search
Provide a query endpoint that can provide search results for any field
in the data with pagination. When multiple fields are specified, the
results should satisfy all conditions.

Request example:

    { "conditions": [
            { "type": "brandName", "values": ["Brother", "Canon"] },
            { "type": "categoryName", "values": ["Printers & Scanners"] }
      ],
      "pagination": { "from": 1, "size": 3 }
    }

Response example:

    [
      {
        "productId": "B01DMYYCD6",
        "title": "Canon EOS 80D DSLR Camera with EF-S 18-55mm f/3.5-5.6 IS STM Lens, Total Of 48GB SDHC along with Deluxe accessory bundle",
        "brandId": "4534",
        "brandName": "Canon",
        "categoryId": "176",
        "categoryName": "Cameras"
        },
      {
        "productId": "B001EQSFRE",
        "title": "Canon Staples P1 (2x5000)",
        "brandId": "4534",
        "brandName": "Canon",
        "categoryId": "191",
        "categoryName": "Home Audio"
      },
      {
        "productId": "B004H9PAO6",
        "title": "Brother TN330 Toner, Standard Yield (Reseller Offer)",
        "brandId": "4053",
        "brandName": "Brother",
        "categoryId": "200",
        "categoryName": "Printers & Scanners"
      }
    ]


### Endpoint #3
#### POST /api/products/keywords
Provide an endpoint that can provide keywords and frequencies from the
product titles given. You may decide how to determine what a keyword is.

Request example:

    { "keywords": ["toner", "ink" ] }

Response example:

    { "keywordFrequencies": [
        { "toner", "25" },
        { "ink", "15" }
      ]
    }

### Endpoint #4
### Design what you want
Each client can receive at most top 10 frequent keywords with out any event request.
The frontend should be able to show the updates without requiring user interation.
{
  "mostFrequent" [
    { "toner", 25 },
    { "ink", 15 },
    { "canon", 10}, 
    .
    .
    .
  ]
}

### Keep in mind ###
* Build the solution as you would build a `real life` application
  * Use any package manager, build chain, library, framework you might use to build such application
  * Consider the design of the different layers in the solution
  * provide tests where applicable
  * Regarding styling, it is not important to do a UX case-study, wireframes, ... but having a nice appearance is definitely something to consider. 
  * Feel free to use any styling idiom/framework you consider.
  * You might guess each field name in `tsv` using Endpoing 2 example.

* Provide how build your solution and test.


