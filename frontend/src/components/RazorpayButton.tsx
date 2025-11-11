"use client";
import { createOrder, verifyPayment } from "@/lib/api";
import { useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL!;

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function RazorpayButton({ plan }: { plan: any }) {
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    document.body.appendChild(script);
  }, []);

  const handlePayment = async () => {
    try {
      const order = await createOrder(plan.price);
      const options = {
        key: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
        amount: order.amount,
        currency: "INR",
        name: "Razorpay Learning",
        description: plan.name,
        order_id: order.order_id,
        handler: async function (response: any) {
          const verifyRes = await verifyPayment(response);
          alert(verifyRes.message);
        },
        modal: {
          ondismiss: async function () {
            console.log("user closed the window");
            await fetch(`${API_URL}/payments/closed`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ order_id: order.orderId }),
            });
          },
        },
        theme: { color: "#3399cc" },
      };

      const razorpay = new window.Razorpay(options);
      razorpay.on("payment.failed", async function (response: any) {
        console.error("Payment Failed", response.error);
        await fetch(`${API_URL}/payments/failed`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            order_id: order.orderId,
            reason: response.error.description,
            code: response.error.code,
          }),
        });
      });
      razorpay.open();
    } catch (error) {
      console.error("Payment initiation failed:", error);
      alert("Something went wrong. Please try again.");
    }
  };
  return (
    <button
      onClick={handlePayment}
      className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
    >
      Buy {plan.name} ₹{plan.price}
    </button>
  );
}
