import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ShoppingCart, Menu, X, BookOpen, User, Search } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { useCart } from '../contexts/CartContext';
import { Link } from 'react-router-dom';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { getCartItemsCount, setIsCartOpen } = useCart();
  const cartItemsCount = getCartItemsCount();

  const menuItems = [
    { name: 'Inicio', href: '/', icon: BookOpen },
    { name: 'Libros', href: '#libros' },
    { name: 'Sobre Mí', href: '#autor' },
    { name: 'Reseñas', href: '#reseñas' },
    { name: 'Contacto', href: '#contacto' }
  ];

  return (
    <motion.header 
      className="fixed top-0 w-full bg-white/90 backdrop-blur-lg z-50 border-b border-gray-100"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center group-hover:scale-105 transition-transform duration-200">
              <BookOpen className="h-6 w-6 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-gray-900">María Fernández</h1>
              <p className="text-xs text-gray-500 -mt-1">Libros de Autoayuda</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {menuItems.map((item, index) => (
              <motion.a
                key={item.name}
                href={item.href}
                className="text-gray-700 hover:text-blue-600 transition-colors duration-200 font-medium relative group"
                whileHover={{ y: -2 }}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                {item.name}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-200 group-hover:w-full"></span>
              </motion.a>
            ))}
          </div>

          {/* Right side buttons */}
          <div className="flex items-center space-x-4">
            {/* Search button - Desktop only */}
            <Button
              variant="ghost"
              size="sm"
              className="hidden md:flex text-gray-600 hover:text-blue-600"
            >
              <Search className="h-4 w-4" />
            </Button>

            {/* Account button - Desktop only */}
            <Button
              variant="ghost"
              size="sm"
              className="hidden md:flex text-gray-600 hover:text-blue-600"
            >
              <User className="h-4 w-4" />
            </Button>

            {/* Cart button */}
            <Link to="/cart">
              <Button
                variant="ghost"
                size="sm"
                className="relative text-gray-600 hover:text-blue-600 hover:bg-blue-50"
              >
                <ShoppingCart className="h-5 w-5" />
                {cartItemsCount > 0 && (
                  <Badge className="absolute -top-2 -right-2 h-5 w-5 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center p-0">
                    {cartItemsCount}
                  </Badge>
                )}
              </Button>
            </Link>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <motion.div
          className={`md:hidden ${isMenuOpen ? 'block' : 'hidden'}`}
          initial={{ opacity: 0, height: 0 }}
          animate={{ 
            opacity: isMenuOpen ? 1 : 0, 
            height: isMenuOpen ? 'auto' : 0 
          }}
          transition={{ duration: 0.3 }}
        >
          <div className="px-2 pt-2 pb-3 space-y-1 bg-white border-t border-gray-100">
            {menuItems.map((item, index) => (
              <motion.a
                key={item.name}
                href={item.href}
                className="flex items-center space-x-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
                onClick={() => setIsMenuOpen(false)}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                {item.icon && <item.icon className="h-5 w-5" />}
                <span>{item.name}</span>
              </motion.a>
            ))}
            
            {/* Mobile search and account */}
            <div className="border-t border-gray-100 pt-3 space-y-1">
              <Button
                variant="ghost"
                className="w-full justify-start text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              >
                <Search className="h-5 w-5 mr-3" />
                Buscar
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              >
                <User className="h-5 w-5 mr-3" />
                Mi Cuenta
              </Button>
            </div>
          </div>
        </motion.div>
      </nav>
    </motion.header>
  );
};

export default Header;