import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: "/",
      component: () => import("../views/DashboardView.vue"),
    },
    {
      path: "/clientes",
      component: () => import("../views/ClientesView.vue"),
    },
    {
      path: "/productos",
      component: () => import("../views/ProductosView.vue"),
    },
    {
      path: "/pedidos",
      component: () => import("../views/PedidosView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/",
    },
  ],
});

export default router;