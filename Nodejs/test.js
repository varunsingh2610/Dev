const https = require('https')

const data = JSON.stringify({
  todo: 'Buy the milk'
})

const options = {
  hostname: 'whatever.com',
  port: 443,
  path: '/todos',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
}

const req = https.request(options, res => {
  console.log(`statusCode: ${res.statusCode}`)

  res.on('data', d => {
    process.stdout.write(d)
  })
})

req.on('error', error => {
  console.error(error)
})

req.write(data)
req.end()



'merchant_id=2&order_id=2&currency=INR&amount=1.00&redirect_url=http%3A%2F%2F127.0.0.1%3A3002%2FccavResponseHandler&cancel_url=http%3A%2F%2F127.0.0.1%3A3002%2FccavResponseHandler&language=EN&billing_name=Peter&billing_address=Santacruz&billing_city=Mumbai&billing_state=MH&billing_zip=400054&billing_country=India&billing_tel=9876543210&billing_email=testing%40domain.com&delivery_name=Sam&delivery_address=Vile%20Parle&delivery_city=Mumbai&delivery_state=Maharashtra&delivery_zip=400038&delivery_country=India&delivery_tel=0123456789&merchant_param1=additional%20Info.&merchant_param2=additional%20Info.&merchant_param3=additional%20Info.&merchant_param4=additional%20Info.&merchant_param5=additional%20Info.&integration_type=iframe_popup&promo_code=&customer_identifier='
