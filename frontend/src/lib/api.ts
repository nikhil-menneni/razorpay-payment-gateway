export const API_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function getPlans() {
  const res = await fetch(`${API_URL}/plans`, { cache: "no-store" });
  return res.json();
}

export async function createOrder(amount: number) {
  const res = await fetch(`${API_URL}/payments/create-order`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount }),
  });
  return res.json();
}

export async function verifyPayment(paymentData: any) {
  console.log(paymentData);
  const res = await fetch(`${API_URL}/payments/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paymentData),
  });
  return res.json();
}
