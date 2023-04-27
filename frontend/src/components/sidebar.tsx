import React from "react";
import { Nav } from "react-bootstrap";

export const Sidebar = () => (
    <section className="side-nav">
      <Nav className="flex-column">
        <Nav.Link className={`side-link ${window.location.pathname === '/' && 'active'}`} href="/">
          Upload
        </Nav.Link>
        <Nav.Link className={`side-link ${window.location.pathname === '/selection' && 'active'}`} href="/selection">
          Selection
        </Nav.Link>
        <Nav.Link className={`side-link ${window.location.pathname === '/information' && 'active'}`} href="/information">
          Additional Information
        </Nav.Link>
      </Nav>
    </section>
  );
