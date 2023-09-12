import stripe
import config

stripe.api_key = config.stripe_secret_key
print(stripe.api_key)



# Create a Price from the product 
price = stripe.Price.create(
  product='prod_OS2KWTzERI9qzb', # product ID
  unit_amount=700,
  currency='usd',
)

# Create subscription using the Price 
subscription = stripe.Subscription.create(
  customer='cus_123',
  items=[
    {
      'price': price.id,
    },
  ],
)

# Create PaymentIntent
intent = stripe.PaymentIntent.create(
  amount=subscription.plan.amount,
  customer=subscription.customer
)

# Create PaymentLink
link = stripe.PaymentLink.create({
  'line_items[0][price]': subscription.items.data[0].price.product, 
  'subscription': subscription.id
})

print(link.url)
