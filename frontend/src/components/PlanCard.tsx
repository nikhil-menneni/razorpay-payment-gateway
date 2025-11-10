import RazorpayButton from "./RazorpayButton";

export default function PlanCard({ plan }: { plan: any }) {
  return (
    <div className="p-5 border rounded-lg shadow-md flex flex-col justify-between">
      <div>
        <h2 className="text-xl font-bold mb-2">{plan.name}</h2>
        <p className="text-gray-600 mb-3">₹{plan.price}</p>
        <ul className="list-disc list-inside text-sm text-gray-500 mb-3">
          {plan.features?.map((f: string, i: number) => (
            <li key={i}>{f}</li>
          ))}
        </ul>
      </div>
      <RazorpayButton plan={plan} />
    </div>
  );
}
