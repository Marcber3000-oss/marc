// Mock data for ebook website
export const mockBooks = [
  {
    id: 1,
    title: "El Poder de la Mentalidad Positiva",
    author: "María Fernández",
    price: 19.99,
    originalPrice: 24.99,
    rating: 4.8,
    reviews: 156,
    cover: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
    description: "Descubre cómo transformar tu vida a través del poder de los pensamientos positivos y la mentalidad ganadora.",
    category: "Desarrollo Personal",
    pages: 256,
    bestseller: true
  },
  {
    id: 2,
    title: "Hábitos que Transforman",
    author: "María Fernández", 
    price: 16.99,
    originalPrice: 21.99,
    rating: 4.9,
    reviews: 203,
    cover: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
    description: "Una guía práctica para crear hábitos positivos que te llevarán al éxito en todas las áreas de tu vida.",
    category: "Productividad",
    pages: 312,
    bestseller: false
  },
  {
    id: 3,
    title: "Supera tus Miedos",
    author: "María Fernández",
    price: 22.99,
    originalPrice: 27.99,
    rating: 4.7,
    reviews: 89,
    cover: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1228&q=80",
    description: "Aprende técnicas probadas para vencer tus miedos y limitaciones, y alcanzar tu máximo potencial.",
    category: "Crecimiento Personal",
    pages: 198,
    bestseller: true
  },
  {
    id: 4,
    title: "Liderazgo Auténtico",
    author: "María Fernández",
    price: 24.99,
    originalPrice: 29.99,
    rating: 4.9,
    reviews: 134,
    cover: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80",
    description: "Desarrolla tu capacidad de liderazgo auténtico y aprende a inspirar y motivar a otros hacia el éxito.",
    category: "Liderazgo", 
    pages: 278,
    bestseller: false
  }
];

export const mockReviews = [
  {
    id: 1,
    author: "Carlos Mendoza",
    title: "Escritor y Coach Personal",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
    review: "María tiene una habilidad única para transformar conceptos complejos en acciones prácticas. Sus libros son una guía invaluable para cualquier persona que busque crecimiento personal.",
    rating: 5,
    bookTitle: "El Poder de la Mentalidad Positiva"
  },
  {
    id: 2,
    author: "Ana García",
    title: "Psicóloga Clínica",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b093?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
    review: "Los libros de María combinan perfectamente la teoría psicológica con ejercicios prácticos. He recomendado sus obras a muchos de mis pacientes con excelentes resultados.",
    rating: 5,
    bookTitle: "Hábitos que Transforman"
  },
  {
    id: 3,
    author: "Roberto Silva",
    title: "CEO de Innovación Empresarial",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
    review: "Como líder empresarial, he encontrado en los libros de María herramientas poderosas que he aplicado tanto en mi vida personal como profesional. Altamente recomendado.",
    rating: 5,
    bookTitle: "Liderazgo Auténtico"
  },
  {
    id: 4,
    author: "Laura Martínez",
    title: "Coach de Vida Certificada",
    avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80",
    review: "María escribe con una claridad y profundidad excepcionales. Sus estrategias para superar miedos han sido transformadoras para mis clientes y para mí misma.",
    rating: 5,
    bookTitle: "Supera tus Miedos"
  }
];

export const mockAuthorInfo = {
  name: "María Fernández",
  title: "Autora de Bestsellers en Desarrollo Personal",
  bio: "María Fernández es una reconocida autora y coach especializada en desarrollo personal con más de 15 años de experiencia. Ha ayudado a miles de personas a transformar sus vidas a través de sus libros, talleres y programas de mentoring. Sus obras han sido traducidas a múltiples idiomas y han alcanzado las listas de bestsellers internacionales.",
  avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b093?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80",
  achievements: [
    "Más de 500,000 libros vendidos mundialmente",
    "Certificada en PNL y Coaching Ontológico", 
    "Conferencista internacional en desarrollo personal",
    "Fundadora de la Academia de Transformación Personal"
  ],
  socialMedia: {
    instagram: "@mariafernandezautor",
    facebook: "MariaFernandezLibros",
    linkedin: "maria-fernandez-autor"
  }
};

export const mockStats = {
  booksPublished: 12,
  readersReached: "500K+",
  averageRating: 4.8,
  countries: 25
};