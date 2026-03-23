# QuickCart API — Bug Reports

## Bug #1: Valid 6-Digit Pincode Rejected
**Endpoint:** `POST /api/v1/addresses`  
**Severity:** High  
**Expected:** A valid 6-digit pincode (e.g., `"500001"`) should be accepted.  
**Actual:** The API returns `{"error": "Invalid pincode"}` for all pincodes, even valid 6-digit ones.  
**Steps:** POST with `{"label":"HOME","street":"12345 Main Street","city":"Hyderabad","pincode":"500001","is_default":false}`

---

## Bug #2: Short Pincode Accepted
**Endpoint:** `POST /api/v1/addresses`  
**Severity:** High  
**Expected:** A 3-digit pincode like `"123"` should be rejected with 400.  
**Actual:** The API returns 200 and accepts the invalid pincode.

---

## Bug #3: Address Update Allows Label Change
**Endpoint:** `PUT /api/v1/addresses/{id}`  
**Severity:** Medium  
**Expected:** Only `street` and `is_default` can be changed. `label` changes should be rejected.  
**Actual:** API returns 200 when attempting to change `label`.

---

## Bug #4: Address Update Allows City Change
**Endpoint:** `PUT /api/v1/addresses/{id}`  
**Severity:** Medium  
**Expected:** `city` changes should be rejected.  
**Actual:** API returns 200 (though it silently ignores the change).

---

## Bug #5: Address Update Allows Pincode Change
**Endpoint:** `PUT /api/v1/addresses/{id}`  
**Severity:** Medium  
**Expected:** `pincode` changes should be rejected.  
**Actual:** API returns 200 (silently ignores the change).

---

## Bug #6: Product Prices Don't Match Admin Database
**Endpoint:** `GET /api/v1/products`  
**Severity:** Critical  
**Expected:** Product prices shown to users must match the real database prices.  
**Actual:** 154+ products have different prices between `/admin/products` and `/products`. Example: Product 8 is 95 in admin but 100 for users.  
**Impact:** Users are being overcharged.

---

## Bug #7: Product Search by Name Doesn't Filter
**Endpoint:** `GET /api/v1/products?name=...`  
**Severity:** Medium  
**Expected:** Searching by name should return only matching products.  
**Actual:** All products are returned regardless of the name search parameter.

---

## Bug #8: Inactive Products Can Be Added to Cart
**Endpoint:** `POST /api/v1/cart/add`  
**Severity:** High  
**Expected:** Adding an inactive product to cart should return 404 or 400.  
**Actual:** API returns 200 `"Item added to cart"` for inactive products.

---

## Bug #9: Cart Accepts Quantity 0
**Endpoint:** `POST /api/v1/cart/add`  
**Severity:** Medium  
**Expected:** Quantity must be at least 1. Sending 0 should return 400.  
**Actual:** API returns 200 `"Item added to cart"` with quantity 0.

---

## Bug #10: Cart Subtotal Calculation Is Wrong
**Endpoint:** `GET /api/v1/cart`  
**Severity:** Critical  
**Expected:** Subtotal for each item should be `quantity × unit_price`.  
**Actual:** Subtotal is completely wrong. Example: 2 × 120 = 240, but API returns -16.

---

## Bug #11: Cart Total Is Always 0 or Incorrect
**Endpoint:** `GET /api/v1/cart`  
**Severity:** Critical  
**Expected:** Cart total should be the sum of all item subtotals.  
**Actual:** Total is always 0 regardless of items in the cart.

---

## Bug #12: Cart Total Wrong With Multiple Items
**Endpoint:** `GET /api/v1/cart`  
**Severity:** Critical  
**Expected:** Total with 2 items should be the sum of both subtotals.  
**Actual:** Total is -16 instead of the correct value (e.g., 370).

---

## Bug #13: Cart Error Message Says ">= 0" Instead of ">= 1"
**Endpoint:** `POST /api/v1/cart/add`  
**Severity:** Low  
**Expected:** Error for negative qty should say "Quantity must be >= 1" (per docs, min is 1).  
**Actual:** Error says "Quantity must be >= 0".

---

## Bug #14: PERCENT Coupon Discount Uses Raw Value, Not Percentage
**Endpoint:** `POST /api/v1/coupon/apply`  
**Severity:** Critical  
**Expected:** PERCENT10 on a cart of 600 should give discount of 60 (10% of 600).  
**Actual:** Discount is 10 (the raw `discount_value`, not computed as percentage).

---

## Bug #15: PERCENT20 Coupon Also Uses Raw Value
**Endpoint:** `POST /api/v1/coupon/apply`  
**Severity:** Critical  
**Expected:** PERCENT20 on a cart of 600 should give discount of 120 (20% of 600).  
**Actual:** Discount is 20 (the raw `discount_value`).

---

## Bug #16: Checkout Allows Empty Cart
**Endpoint:** `POST /api/v1/checkout`  
**Severity:** High  
**Expected:** Checkout with an empty cart should return 400.  
**Actual:** API returns 200 and creates an order with total_amount 0.

---

## Bug #17: Wallet Pay Deducts Wrong Amount
**Endpoint:** `POST /api/v1/wallet/pay`  
**Severity:** High  
**Expected:** Paying 50 from wallet should deduct exactly 50.  
**Actual:** Balance drops by ~50.4 instead of exactly 50. Extra money is being taken.

---

## Bug #18: Delivered Order Can Be Cancelled
**Endpoint:** `POST /api/v1/orders/{id}/cancel`  
**Severity:** High  
**Expected:** Cancelling a delivered order should return 400.  
**Actual:** API returns 200 and cancels the delivered order.

---

## Bug #19: Order Cancellation Doesn't Restock Items
**Endpoint:** `POST /api/v1/orders/{id}/cancel`  
**Severity:** Critical  
**Expected:** When an order is cancelled, all items should be added back to product stock.  
**Actual:** Stock remains reduced after cancellation. Example: stock was 282, ordered 2 (→280), cancelled, stock stays at 280.

---

## Bug #20: Review Average Rating Is Integer Instead of Decimal
**Endpoint:** `GET /api/v1/products/{id}/reviews`  
**Severity:** Medium  
**Expected:** Average rating should be a proper decimal (e.g., 3.4).  
**Actual:** Average rating is rounded down to an integer (e.g., 3).

---

## Bug #21: Support Ticket CLOSED → OPEN Transition Allowed
**Endpoint:** `PUT /api/v1/support/tickets/{id}`  
**Severity:** Medium  
**Expected:** Status transitions should only go OPEN → IN_PROGRESS → CLOSED. Reverse not allowed.  
**Actual:** API allows transitioning from CLOSED back to OPEN.

---

## Bug #22: Support Ticket CLOSED → IN_PROGRESS Transition Allowed
**Endpoint:** `PUT /api/v1/support/tickets/{id}`  
**Severity:** Medium  
**Expected:** CLOSED tickets cannot go to IN_PROGRESS.  
**Actual:** API allows it and returns 200.

---

## Bug #23: Profile Phone Accepts Letters Instead of Digits
**Endpoint:** `PUT /api/v1/profile`  
**Severity:** Medium  
**Expected:** Phone must be exactly 10 digits. `"abcdefghij"` should be rejected with 400.  
**Actual:** API accepts the letters-only phone number and returns 200.
