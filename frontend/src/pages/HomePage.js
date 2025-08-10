import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Star, ShoppingCart, BookOpen, Users, Award, TrendingUp } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { useCart } from '../contexts/CartContext';
import { mockBooks, mockReviews, mockAuthorInfo, mockStats } from '../mock';
import { useToast } from '../hooks/use-toast';
import Header from '../components/Header';
import Footer from '../components/Footer';

const HomePage = () => {
  const { addToCart } = useCart();
  const { toast } = useToast();
  const [featuredBooks, setFeaturedBooks] = useState([]);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    // Simulate API call with mock data
    setFeaturedBooks(mockBooks);
    setReviews(mockReviews);
  }, []);

  const handleAddToCart = (book) => {
    addToCart(book);
    toast({
      title: "¡Agregado al carrito!",
      description: `"${book.title}" se agregó a tu carrito.`,
      duration: 3000,
    });
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 50, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
        ease: "easeOut"
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <Header />
      
      {/* Hero Section */}
      <motion.section 
        className="relative pt-32 pb-20 px-4"
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div variants={itemVariants} className="space-y-8">
              <div className="space-y-4">
                <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-200 px-4 py-2">
                  ✨ Bestsellers en Desarrollo Personal
                </Badge>
                <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight">
                  Transforma tu
                  <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                    {" "}Vida{" "}
                  </span>
                  con Cada Página
                </h1>
                <p className="text-xl text-gray-600 leading-relaxed">
                  Descubre los secretos del desarrollo personal con los libros de María Fernández. 
                  Más de 500,000 lectores ya han transformado sus vidas.
                </p>
              </div>
              
              <div className="flex flex-wrap gap-4">
                <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                  <BookOpen className="mr-2 h-5 w-5" />
                  Explorar Libros
                </Button>
                <Button size="lg" variant="outline" className="border-blue-200 text-blue-700 hover:bg-blue-50 px-8 py-4 text-lg">
                  Sobre la Autora
                </Button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-8">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{mockStats.booksPublished}</div>
                  <div className="text-sm text-gray-600">Libros Publicados</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{mockStats.readersReached}</div>
                  <div className="text-sm text-gray-600">Lectores</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{mockStats.averageRating}</div>
                  <div className="text-sm text-gray-600">Puntuación</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{mockStats.countries}</div>
                  <div className="text-sm text-gray-600">Países</div>
                </div>
              </div>
            </motion.div>

            <motion.div variants={itemVariants} className="relative">
              <div className="relative">
                <img
                  src={mockAuthorInfo.avatar}
                  alt="María Fernández"
                  className="rounded-2xl shadow-2xl w-full max-w-md mx-auto"
                />
                <div className="absolute -bottom-6 -right-6 bg-white rounded-xl p-4 shadow-lg">
                  <div className="flex items-center gap-2">
                    <Star className="h-5 w-5 text-yellow-400 fill-current" />
                    <span className="font-semibold">4.8/5</span>
                    <span className="text-gray-500 text-sm">Puntuación promedio</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Featured Books Section */}
      <motion.section 
        className="py-20 px-4 bg-white"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={containerVariants}
      >
        <div className="max-w-7xl mx-auto">
          <motion.div variants={itemVariants} className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Libros Destacados
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Cada libro es una puerta hacia una nueva versión de ti mismo. 
              Explora nuestra colección de bestsellers en desarrollo personal.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {featuredBooks.map((book, index) => (
              <motion.div
                key={book.id}
                variants={itemVariants}
                whileHover={{ y: -8, transition: { duration: 0.2 } }}
                className="group"
              >
                <Card className="h-full shadow-lg hover:shadow-2xl transition-all duration-300 border-0 bg-gradient-to-br from-white to-gray-50">
                  <CardHeader className="p-0">
                    <div className="relative overflow-hidden rounded-t-lg">
                      {book.bestseller && (
                        <Badge className="absolute top-4 left-4 z-10 bg-red-500 text-white">
                          <TrendingUp className="w-3 h-3 mr-1" />
                          Bestseller
                        </Badge>
                      )}
                      <img
                        src={book.cover}
                        alt={book.title}
                        className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    </div>
                  </CardHeader>
                  <CardContent className="p-6 space-y-4">
                    <div>
                      <Badge variant="outline" className="text-blue-600 border-blue-200 mb-2">
                        {book.category}
                      </Badge>
                      <h3 className="font-bold text-lg text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors">
                        {book.title}
                      </h3>
                      <p className="text-gray-600 text-sm mt-2 line-clamp-2">
                        {book.description}
                      </p>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="flex items-center">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < Math.floor(book.rating)
                                  ? 'text-yellow-400 fill-current'
                                  : 'text-gray-300'
                              }`}
                            />
                          ))}
                        </div>
                        <span className="text-sm text-gray-600">({book.reviews})</span>
                      </div>
                      <span className="text-sm text-gray-500">{book.pages} páginas</span>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl font-bold text-blue-600">
                          ${book.price}
                        </span>
                        <span className="text-sm text-gray-400 line-through">
                          ${book.originalPrice}
                        </span>
                      </div>
                    </div>

                    <Button
                      onClick={() => handleAddToCart(book)}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white group-hover:shadow-lg transition-all duration-300"
                    >
                      <ShoppingCart className="mr-2 h-4 w-4" />
                      Agregar al Carrito
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Reviews Section */}
      <motion.section 
        className="py-20 px-4 bg-gradient-to-br from-blue-50 to-indigo-100"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={containerVariants}
      >
        <div className="max-w-7xl mx-auto">
          <motion.div variants={itemVariants} className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Lo Que Dicen los Expertos
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Profesionales reconocidos en psicología, coaching y desarrollo personal 
              respaldan la calidad y efectividad de estos libros.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8">
            {reviews.map((review, index) => (
              <motion.div
                key={review.id}
                variants={itemVariants}
                whileHover={{ y: -4, transition: { duration: 0.2 } }}
              >
                <Card className="h-full shadow-lg hover:shadow-2xl transition-all duration-300 border-0 bg-white">
                  <CardContent className="p-8 space-y-4">
                    <div className="flex items-center gap-1 mb-4">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className="w-5 h-5 text-yellow-400 fill-current"
                        />
                      ))}
                    </div>
                    
                    <p className="text-gray-700 italic text-lg leading-relaxed">
                      "{review.review}"
                    </p>
                    
                    <div className="flex items-center gap-4 pt-4">
                      <Avatar className="w-12 h-12">
                        <AvatarImage src={review.avatar} alt={review.author} />
                        <AvatarFallback>{review.author.charAt(0)}</AvatarFallback>
                      </Avatar>
                      <div>
                        <h4 className="font-semibold text-gray-900">{review.author}</h4>
                        <p className="text-blue-600 text-sm">{review.title}</p>
                        <p className="text-gray-500 text-sm">Sobre "{review.bookTitle}"</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Author Section */}
      <motion.section 
        className="py-20 px-4 bg-white"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={containerVariants}
      >
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div variants={itemVariants}>
              <img
                src={mockAuthorInfo.avatar}
                alt={mockAuthorInfo.name}
                className="rounded-2xl shadow-2xl w-full max-w-md mx-auto"
              />
            </motion.div>

            <motion.div variants={itemVariants} className="space-y-6">
              <div>
                <h2 className="text-4xl font-bold text-gray-900 mb-2">
                  Conoce a {mockAuthorInfo.name}
                </h2>
                <p className="text-xl text-blue-600 font-semibold mb-6">
                  {mockAuthorInfo.title}
                </p>
                <p className="text-lg text-gray-700 leading-relaxed">
                  {mockAuthorInfo.bio}
                </p>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                  <Award className="h-5 w-5 text-blue-600" />
                  Logros Destacados
                </h3>
                <ul className="space-y-2">
                  {mockAuthorInfo.achievements.map((achievement, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-blue-600 rounded-full mt-3 flex-shrink-0"></div>
                      <span className="text-gray-700">{achievement}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white">
                <Users className="mr-2 h-5 w-5" />
                Conectar en Redes Sociales
              </Button>
            </motion.div>
          </div>
        </div>
      </motion.section>

      <Footer />
    </div>
  );
};

export default HomePage;