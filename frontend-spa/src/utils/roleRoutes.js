export function dashboardRouteForRole(role) {
  if (role === "admin") {
    return { name: "dashboardAdmin" }
  }

  if (role === "manager") {
    return { name: "dashboardManager" }
  }

  // Fallback and "superadmin" role lands on the main dashboard view
  return { name: "dashboard" }
}
