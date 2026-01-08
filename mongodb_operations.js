// Operation 1: Load Data (Mock command)
// mongoimport --db fleximart --collection products --file products_catalog.json

// Operation 2: Basic Query
// Find Electronics under 50,000, show only Name and Price
db.products.find(
    { category: "Electronics", price: { $lt: 50000 } },
    { name: 1, price: 1, stock: 1, _id: 0 }
);

// Operation 3: Review Analysis
// Find products with Avg Rating >= 4.0
db.products.aggregate([
    { $unwind: "$reviews" },
    { $group: {
        _id: "$_id",
        name: { $first: "$name" },
        avg_rating: { $avg: "$reviews.rating" }
    }},
    { $match: { avg_rating: { $gte: 4.0 } } }
]);

// Operation 4: Update Operation
// Add a new review to product ELEC001
db.products.updateOne(
    { product_id: "ELEC001" },
    { $push: { 
        reviews: {
            user: "U999",
            rating: 4,
            comment: "Excellent battery life",
            date: new Date()
        } 
    }}
);

// Operation 5: Complex Aggregation
// Average Price per Category
db.products.aggregate([
    { $group: {
        _id: "$category",
        avg_price: { $avg: "$price" },
        total_products: { $sum: 1 }
    }},
    { $sort: { avg_price: -1 } }
]);