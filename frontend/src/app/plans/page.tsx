import { getPlans } from "@/lib/api";
import PlanCard from "@/components/PlanCard";

export default async function PlansPage() {
  const data = await getPlans();
  const plans = data.plans || [];
  return (
    <div>
      {plans.map((plan: any) => (
        <PlanCard key={plan.id} plan={plan} />
      ))}
    </div>
  );
}
