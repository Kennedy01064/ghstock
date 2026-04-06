export function dashboardRouteForRole(role) {
  if (role === "admin") {
    return { name: "dashboardAdmin" }
  }

  if (role === "manager") {
    return { name: "dashboardManager" }
  }

  return { name: "dashboard" }
}
