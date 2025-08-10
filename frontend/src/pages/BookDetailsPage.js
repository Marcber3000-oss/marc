import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Star, ShoppingCart, BookOpen, Clock, Award, Share2 } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { useCart } from '../contexts/CartContext';
import { useToast } from '../hooks/use-toast';
import { mockBooks, mockReviews } from '../mock';
import Header from '../components/Header';
import Footer from '../components/Footer';

const BookDetailsPage = () => {
  const { id } = useParams();
  const { addToCart } = useCart();
  const { toast } = useToast();
  const [book, setBook] = useState(null);
  const [relatedBooks, setRelatedBooks] = useState([]);
  const [bookReviews, setBookReviews] = useState([]);

  useEffect(() => {
    // Find the book by ID
    const foundBook = mockBooks.find(b => b.id === parseInt(id));
    setBook(foundBook);

    // Get related books (same category, different book)
    if (foundBook) {
      const related = mockBooks.filter(b => 
        b.category === foundBook.category && b.id !== foundBook.id
      ).slice(0, 3);
      setRelatedBooks(related);

      // Get reviews for this book
      const reviews = mockReviews.filter(r => r.bookTitle === foundBook.title);
      setBookReviews(reviews);
    }
  }, [id]);

  const handleAddToCart = () => {
    addToCart(book);
    toast({
      title: "¡Agregado al carrito!",
      description: `"${book.title}" se agregó a tu carrito.`,
      duration: 3000,
    });
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: book.title,
        text: book.description,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      toast({
        title: "¡Enlace copiado!",
        description: "El enlace ha sido copiado al portapapeles.",
        duration: 2000,
      });
    }
  };

  if (!book) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Libro no encontrado</h2>
          <Link to="/" className="text-blue-600 hover:text-blue-700">
            Volver al inicio
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <Header />

      <main className="pt-20 pb-12">
        <div className="max-w-7xl mx-auto px-4">
          {/* Back Button */}
          <motion.div 
            className="mb-8"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Link to="/">
              <Button variant="ghost" className="text-gray-600 hover:text-blue-600">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Volver a la tienda
              </Button>
            </Link>
          </motion.div>

          {/* Book Details */}
          <div className="grid lg:grid-cols-2 gap-12 mb-16">
            {/* Book Cover */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
            >
              <div className="relative">
                <img
                  src={book.cover}
                  alt={book.title}
                  className="w-full max-w-md mx-auto rounded-2xl shadow-2xl"
                />
                {book.bestseller && (
                  <Badge className="absolute top-4 left-4 bg-red-500 text-white px-3 py-1">
                    <Award className="w-3 h-3 mr-1" />
                    Bestseller
                  </Badge>
                )}
              </div>
            </motion.div>

            {/* Book Info */}
            <motion.div 
              className="space-y-6"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div>
                <Badge className="text-blue-600 border-blue-200 mb-3">
                  {book.category}
                </Badge>
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  {book.title}
                </h1>
                <p className="text-xl text-gray-600 mb-4">
                  Por {book.author}
                </p>
                <p className="text-lg text-gray-700 leading-relaxed">
                  {book.description}
                </p>
              </div>

              {/* Rating and Reviews */}
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-5 h-5 ${
                          i < Math.floor(book.rating)
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <span className="text-lg font-semibold">{book.rating}</span>
                  <span className="text-gray-600">({book.reviews} reseñas)</span>
                </div>
              </div>

              {/* Book Stats */}
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center gap-2 text-gray-600">
                  <BookOpen className="h-5 w-5" />
                  <span>{book.pages} páginas</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Clock className="h-5 w-5" />
                  <span>Descarga instantánea</span>
                </div>
              </div>

              {/* Price and Actions */}
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <span className="text-3xl font-bold text-blue-600">
                    ${book.price}
                  </span>
                  <span className="text-xl text-gray-400 line-through">
                    ${book.originalPrice}
                  </span>
                  <Badge variant="destructive">
                    Oferta limitada
                  </Badge>
                </div>

                <div className="flex flex-col sm:flex-row gap-3">
                  <Button
                    size="lg"
                    onClick={handleAddToCart}
                    className="bg-blue-600 hover:bg-blue-700 text-white flex-1"
                  >
                    <ShoppingCart className="mr-2 h-5 w-5" />
                    Agregar al Carrito
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={handleShare}
                    className="border-blue-200 text-blue-700 hover:bg-blue-50"
                  >
                    <Share2 className="mr-2 h-5 w-5" />
                    Compartir
                  </Button>
                </div>
              </div>

              {/* Guarantees */}
              <div className="bg-blue-50 rounded-lg p-4 space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Garantía de satisfacción de 30 días</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Descarga inmediata tras la compra</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Formato PDF compatible con todos los dispositivos</span>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Book Reviews */}
          {bookReviews.length > 0 && (
            <motion.section 
              className="mb-16"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
                Reseñas de Expertos
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                {bookReviews.map((review) => (
                  <Card key={review.id} className="shadow-lg">
                    <CardContent className="p-6">
                      <div className="flex items-center gap-1 mb-4">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className="w-4 h-4 text-yellow-400 fill-current"
                          />
                        ))}
                      </div>
                      <p className="text-gray-700 italic mb-4">"{review.review}"</p>
                      <div className="flex items-center gap-3">
                        <img
                          src={review.avatar}
                          alt={review.author}
                          className="w-10 h-10 rounded-full"
                        />
                        <div>
                          <h4 className="font-semibold text-gray-900">{review.author}</h4>
                          <p className="text-blue-600 text-sm">{review.title}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </motion.section>
          )}

          {/* Related Books */}
          {relatedBooks.length > 0 && (
            <motion.section
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
                Libros Relacionados
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                {relatedBooks.map((relatedBook) => (
                  <Card key={relatedBook.id} className="shadow-lg hover:shadow-xl transition-shadow">
                    <CardContent className="p-0">
                      <Link to={`/book/${relatedBook.id}`}>
                        <img
                          src={relatedBook.cover}
                          alt={relatedBook.title}
                          className="w-full h-64 object-cover rounded-t-lg hover:scale-105 transition-transform duration-300"
                        />
                        <div className="p-6">
                          <h3 className="font-bold text-lg text-gray-900 mb-2">
                            {relatedBook.title}
                          </h3>
                          <div className="flex items-center justify-between">
                            <span className="text-xl font-bold text-blue-600">
                              ${relatedBook.price}
                            </span>
                            <div className="flex items-center">
                              <Star className="w-4 h-4 text-yellow-400 fill-current" />
                              <span className="ml-1 text-sm text-gray-600">
                                {relatedBook.rating}
                              </span>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </motion.section>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default BookDetailsPage;