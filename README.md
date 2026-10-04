# CRUD Vue 3 + Flask

Aplicación CRUD desarrollada para Windows utilizando Vue 3,
Vue Router, Axios, Flask y Flask-SQLAlchemy.

## Tecnologías utilizadas

### Frontend

- Vue 3
- Vue Router
- Axios
- Bootstrap
- Vite

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite

## Funcionalidades

La aplicación permite administrar:

- Clientes
- Productos
- Pedidos

Cada módulo permite realizar operaciones CRUD:

- Crear
- Consultar
- Actualizar
- Eliminar

## Estructura del proyecto

```text
crud-vue-flask/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── clientes.py
│   │   │   ├── productos.py
│   │   │   └── pedidos.py
│   │   │
│   │   ├── __init__.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── errors.py
│   │
│   ├── migrations/
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   ├── requirements-lock.txt
│   └── run.py
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── DataTable.vue
    │   │   ├── FormField.vue
    │   │   ├── LoadingMessage.vue
    │   │   └── AlertMessage.vue
    │   │
    │   ├── router/
    │   ├── services/
    │   ├── views/
    │   │   ├── DashboardView.vue
    │   │   ├── ClientesView.vue
    │   │   ├── ProductosView.vue
    │   │   └── PedidosView.vue
    │   │
    │   ├── App.vue
    │   └── main.js
    │
    └── package.json