import TR28.Counting
import TR28.LinearCount
import TR28.Isolation
import TR28.Density

namespace TR28

/-- The conjunction of every target in the frozen core contract. -/
theorem core_theorems : CoreTheorems :=
  ⟨partner_position_count, partner_histogram_count, balanced_partner_count,
   exact_span_partner_subset, exact_span_partner_bound, finite_field_kernel_count,
   isolation_count, exact_coordinate_extraction, uniform_isolation_extraction,
   invariant_supermodular_density⟩

end TR28
