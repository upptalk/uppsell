# UPPSELL

A django-based Restful API for business objects relating to e-commerce
and an admin for managing them.

## Features

- Order and payment workflows allow you to assign custom callbacks at different
  stages of the order cycle, such as:
  - provision a service only once a payment is made
  - check that a transition can be made
  - generate an invoice
  - email a customer

### Order workflow diagram

![Order States](doc/order_states.png "Order States")


### Payment workflow diagram

![Payment States](doc/payment_states.png "Payment States")

## Legal
- License: [MIT](LICENSE.txt)
- Copyright: Copyright © 2014 [yuilop SL](http://yuilop.com)

## Credits

- Adam Hayward <adam (at) upptalk /dot/ com>
- Francesc Vendrell <francesc (at) upptalk /dot/ com>
