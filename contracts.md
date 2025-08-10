# Contratos API y Plan de Integración Backend-Frontend

## 1. API Contracts (Endpoints Backend)

### Books API
```
GET /api/books
- Retorna: Lista de todos los libros
- Response: Array de objetos Book

GET /api/books/:id  
- Retorna: Detalles de un libro específico
- Response: Objeto Book

POST /api/books (Admin)
- Crea nuevo libro
- Body: BookCreate object
```

### Orders API  
```
POST /api/orders
- Crea una nueva orden de compra
- Body: { items: [BookOrder], customerInfo: CustomerInfo, paymentInfo: PaymentInfo }
- Response: { orderId, paymentUrl, status }

GET /api/orders/:orderId
- Retorna detalles de una orden
- Response: Order object con downloadLinks

POST /api/orders/:orderId/download
- Genera enlaces de descarga para libros comprados
- Response: { downloadLinks: [{ bookId, downloadUrl, expiresAt }] }
```

### Reviews API
```
GET /api/reviews
- Retorna todas las reseñas de expertos
- Response: Array de Review objects

GET /api/reviews/book/:bookId
- Retorna reseñas específicas de un libro
- Response: Array de Review objects
```

### Author API
```
GET /api/author
- Retorna información de la autora
- Response: Author object con bio, achievements, stats
```

### Payment Integration (Stripe)
```
POST /api/payments/create-intent
- Crea PaymentIntent de Stripe
- Body: { amount, orderId }
- Response: { clientSecret, paymentIntentId }

POST /api/payments/confirm
- Confirma pago exitoso y activa descargas
- Body: { paymentIntentId, orderId }
- Response: { success, downloadLinks }
```

## 2. Datos Mock a Reemplazar

### Frontend Mock Data (mock.js):
- `mockBooks` → Reemplazar con `GET /api/books`
- `mockReviews` → Reemplazar con `GET /api/reviews`  
- `mockAuthorInfo` → Reemplazar con `GET /api/author`
- `mockStats` → Calculados dinámicamente en backend

### Funciones Mock a Reemplazar:
- `addToCart()` → Mantener en frontend (localStorage)
- Checkout process → Integrar con Stripe real
- Order completion → Llamar APIs reales

## 3. Implementación Backend

### Modelos MongoDB:
```python
# Book Model
{
  _id: ObjectId,
  title: str,
  author: str,
  price: float,
  originalPrice: float,
  description: str,
  category: str,
  cover: str,
  pages: int,
  rating: float,
  reviewCount: int,
  bestseller: bool,
  fileUrl: str, # Enlace al PDF del libro
  createdAt: datetime,
  updatedAt: datetime
}

# Order Model  
{
  _id: ObjectId,
  orderId: str, # ID único para el usuario
  items: [{ bookId: ObjectId, quantity: int, price: float }],
  customer: { 
    email: str,
    firstName: str, 
    lastName: str,
    country: str 
  },
  paymentInfo: {
    paymentIntentId: str,
    amount: float,
    status: str, # pending, completed, failed
    paymentMethod: str
  },
  downloadLinks: [{ 
    bookId: ObjectId, 
    downloadUrl: str, 
    expiresAt: datetime 
  }],
  status: str, # pending, paid, delivered
  createdAt: datetime,
  updatedAt: datetime
}

# Review Model
{
  _id: ObjectId,
  author: str,
  title: str, # Título profesional del reviewer
  avatar: str,
  review: str,
  rating: int,
  bookId: ObjectId, # Referencia al libro
  bookTitle: str,
  featured: bool, # Si aparece en homepage
  createdAt: datetime
}

# Author Model (Singleton)
{
  _id: ObjectId,
  name: str,
  title: str,
  bio: str,
  avatar: str,
  achievements: [str],
  socialMedia: { instagram: str, facebook: str, linkedin: str },
  stats: { 
    booksPublished: int,
    readersReached: str,
    averageRating: float,
    countries: int
  }
}
```

### Stripe Integration:
- Configurar webhook para confirmación de pagos
- Generar enlaces de descarga seguros con expiración
- Enviar emails automáticos post-compra

## 4. Plan de Integración Frontend-Backend

### Fase 1: Reemplazar Mock Data
1. Crear hook `useApi.js` para llamadas HTTP
2. Reemplazar `mockBooks` en HomePage con `GET /api/books`
3. Reemplazar `mockReviews` con `GET /api/reviews`
4. Actualizar BookDetailsPage para usar `GET /api/books/:id`

### Fase 2: Sistema de Pagos
1. Instalar `@stripe/stripe-js` en frontend
2. Reemplazar checkout mock con Stripe Elements
3. Integrar confirmación de pago real
4. Mostrar página de éxito con enlaces de descarga

### Fase 3: Gestión de Órdenes
1. Crear página "Mis Compras" para usuarios
2. Sistema de re-descarga de libros comprados
3. Email automation post-compra

### Archivos Frontend a Modificar:
- `src/pages/HomePage.js` → Usar APIs reales
- `src/pages/BookDetailsPage.js` → Usar API real
- `src/pages/CheckoutPage.js` → Integrar Stripe
- `src/hooks/useApi.js` → Nuevo hook para APIs
- `src/components/StripeCheckout.js` → Nuevo componente

### Variables de Entorno:
```
STRIPE_PUBLIC_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## 5. Características de Seguridad

- Enlaces de descarga con JWT tokens
- Expiración automática de downloads (24-48 horas)
- Validación de compras antes de permitir descargas
- Rate limiting en endpoints sensibles
- Validación de pagos con Stripe webhooks