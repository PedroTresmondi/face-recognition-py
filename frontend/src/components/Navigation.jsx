import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav className="bg-gray-800 p-4 w-full">
      <ul className="flex space-x-4 justify-center">
        <li>
          <Link
            to="/auth"
            className="text-white bg-blue-500 hover:bg-green-600 px-4 py-2 rounded transition duration-300"
          >
            Auth
          </Link>
        </li>
        <li>
          <Link
            to="/register"
            className="text-white bg-blue-500 hover:bg-green-600 px-4 py-2 rounded transition duration-300"
          >
            Register
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;
