# Design Challenge 2

## Description
A tool to visualize complex knowledge from the product information and review information. The application takes a product information file and review information file and generates visualization to solve complex tasks for seller and buyer.

## Web Application

* URL - https://data-vis-dc2.herokuapp.com/
* Video URL -  https://youtu.be/Evja03HMLiA

The application takes input data file at startup time. Since this is a predeployed application, it only shows visualization for the Musical Instruments dataset.


## Libraries used

* Python
* Panda
* Dash
* Plotly

## Setup

This program take two input filess
1) Review details file. We will call it file1.
2) Product detail file. We will call it file2.

If you don't provide these files, it will automatically start with Musical Instruments dataset.

### Run locally
Execute the following commands
```
* git clone https://github.com/anshuv99/data-vis.git
* pip install -r requirements.txt
* python final_handing.py $path_to_file1 $path_to_file2
* Open URL http://127.0.0.1:8050/
```

## Snapshots
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/Product_detail_graph.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/overall_ratying_review.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/rating_distribution_over_time.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/rating_review_count_category.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/review_distribution_over_time.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/tredning_peoduct_active_reviewers.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/customer_giving_low_rating_high_rating.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/Focusing_on_major_selling_item_distribution.png)
![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/parallel_coordinates_dimension_product.png)

![Image of Yaktocat](https://github.com/anshuv99/data-vis/blob/master/snaphots/Focusing_on_specific_price_range_and_category.png)
