import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'tdesign-react';
import Dashboard from './pages/Dashboard';
import ProductManagement from './pages/ProductManagement';
import OrderManagement from './pages/OrderManagement';

const { Header, Content, Footer, Sider } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Sider>
          <Menu>
            <Menu.MenuItem value="dashboard">
              <Link to="/">仪表盘</Link>
            </Menu.MenuItem>
            <Menu.MenuItem value="products">
              <Link to="/products">商品管理</Link>
            </Menu.MenuItem>
            <Menu.MenuItem value="orders">
              <Link to="/orders">订单管理</Link>
            </Menu.MenuItem>
          </Menu>
        </Sider>
        <Layout>
          <Header>Header</Header>
          <Content>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/products" element={<ProductManagement />} />
              <Route path="/orders" element={<OrderManagement />} />
            </Routes>
          </Content>
          <Footer>Footer</Footer>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App;
