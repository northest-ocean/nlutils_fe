import Vue from "vue";
import VueRouter from "vue-router";
import Data from "../views/Data.vue";
import Index from "../views/Index.vue";
import Project from "../views/Project.vue";
import Training from "../views/Training.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Project Index Page",
    component: Index,
  },
  {
    path: "/project",
    name: "Project Detail Page",
    component: Project,
  },
  {
    path: "/data",
    name: "Data",
    component: Data,
  },
  {
    path: "/training",
    name: "Training Tables",
    component: Training,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
