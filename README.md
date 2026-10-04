# CRUD Vue 3 + Flask

Aplicación CRUD desarrollada para Windows utilizando Vue 3, Vue Router, Axios, Bootstrap, Flask y Flask-SQLAlchemy.

## Tecnologías utilizadas

### Frontend

* Vue 3
* Vue Router
* Axios
* Bootstrap 5
* Vite

### Backend

* Python
* Flask
* Flask-Cors
* Flask-SQLAlchemy
* Flask-Migrate
* python-dotenv
* pytest
* SQLite

## Funcionalidades

La aplicación permite administrar:

* Clientes
* Productos
* Pedidos

Incluye operaciones de:

* Crear
* Consultar
* Actualizar
* Eliminar

También incluye validaciones en frontend y backend, manejo de errores y estados de carga.

## Estructura del proyecto

```text
crud-vue-flask/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── clientes.py
│   │   │   ├── productos.py
│   │   │   └── pedidos.py
│   │   ├── __init__.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── errors.py
│   ├── migrations/
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   ├── requirements-lock.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DataTable.vue
│   │   │   ├── FormField.vue
│   │   │   ├── LoadingMessage.vue
│   │   │   └── AlertMessage.vue
│   │   ├── router/
│   │   ├── services/
│   │   ├── views/
│   │   │   ├── DashboardView.vue
│   │   │   ├── ClientesView.vue
│   │   │   ├── ProductosView.vue
│   │   │   └── PedidosView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env.example
│   └── package.json
│
└── README.md
```

## Requisitos

* Windows
* Python
* Node.js
* npm
* PostgreSQL o SQLite según la configuración del proyecto

## Configuración del backend

Entrar a la carpeta del backend:

```powershell
cd backend
```

Crear y activar el entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

Configurar las variables de entorno utilizando `.env.example` como referencia.

## Migraciones de la base de datos

Desde la carpeta `backend`:

```powershell
flask --app run.py db upgrade
```

Si se necesitan crear nuevas migraciones:

```powershell
flask --app run.py db migrate -m "descripcion del cambio"
```

Luego:

```powershell
flask --app run.py db upgrade
```

## Ejecutar el backend

Desde la carpeta `backend`:

```powershell
flask --app run.py run --debug
```

El backend estará disponible en:

```text
http://127.0.0.1:5000
```

## Configuración del frontend

Entrar a la carpeta del frontend:

```powershell
cd frontend
```

Instalar las dependencias:

```powershell
npm install
```

Crear el archivo `.env` a partir de `.env.example`:

```env
VITE_API_URL=http://127.0.0.1:5000/api
```

## Ejecutar el frontend

Desde la carpeta `frontend`:

```powershell
npm run dev
```

Vite mostrará la dirección local para acceder a la aplicación.

## Rutas principales

### Frontend

* `/dashboard`
* `/clientes`
* `/productos`
* `/pedidos`

Las rutas inexistentes son redirigidas al dashboard.

### API

```text
GET    /api/clientes
POST   /api/clientes
GET    /api/clientes/<id>
PUT    /api/clientes/<id>
DELETE /api/clientes/<id>

GET    /api/productos
POST   /api/productos
GET    /api/productos/<id>
PUT    /api/productos/<id>
DELETE /api/productos/<id>

GET    /api/pedidos
POST   /api/pedidos
GET    /api/pedidos/<id>
PUT    /api/pedidos/<id>
DELETE /api/pedidos/<id>

GET    /health
```

## Componentes reutilizables

El frontend utiliza componentes reutilizables para evitar repetir código:

* `DataTable.vue`: muestra información en tablas.
* `FormField.vue`: reutiliza campos de formularios.
* `LoadingMessage.vue`: muestra estados de carga.
* `AlertMessage.vue`: muestra mensajes de éxito y error.

## Validaciones

El sistema realiza validaciones en frontend y backend.

Entre ellas:

* Campos obligatorios.
* Cantidades mayores que cero.
* Precio y stock válidos.
* Existencia del cliente.
* Existencia del producto.
* Validación de stock disponible.
* Estados válidos para los pedidos.

Los estados permitidos para los pedidos son:

```text
pendiente
pagado
enviado
cancelado
```

Los pedidos solamente pueden eliminarse cuando están en estado `cancelado`.

## Pruebas

Las pruebas del backend se ejecutan con:

```powershell
pytest
```

Actualmente se incluyen pruebas para clientes y productos.

Resultado esperado:

```text
2 passed
```

## Arquitectura

La aplicación utiliza una arquitectura separada en frontend y backend.

El frontend está desarrollado con Vue 3 y se encarga de la interfaz, navegación, formularios y consumo de la API mediante Axios.

El backend está desarrollado con Flask y proporciona una API REST para administrar clientes, productos y pedidos.

Flask-SQLAlchemy permite trabajar con los modelos de la base de datos y Flask-Migrate permite administrar las migraciones.

## Variables de entorno

Los archivos `.env` contienen configuraciones locales y no deben incluirse en el repositorio.

Se proporciona un archivo `.env.example` como referencia para configurar el proyecto.

## Repositorio

El código fuente del proyecto se encuentra en GitHub:

`https://github.com/Eddy-Arana/crud-vue-flask`
