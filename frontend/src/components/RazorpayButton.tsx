"use client";
import { createOrder, verifyPayment } from "@/lib/api";
import { useEffect } from "react";

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
    const order = await createOrder(plan.price);
    const options = {
      key: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
      amount: plan.price * 100,
      currency: "INR",
      name: "Razorpay Learning",
      description: plan.name,
      order_id: order.order_id,
      handler: async function (response: any) {
        const verifyRes = await verifyPayment(response);
        alert(verifyRes.message);
      },
      theme: { color: "#3399cc" },
    };

    const razorpay = new window.Razorpay(options);
    razorpay.open();
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
