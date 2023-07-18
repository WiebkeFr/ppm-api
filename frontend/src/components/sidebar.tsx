import React from "react";
import { Nav } from "react-bootstrap";

const pages = [
  {
    href: "",
    label: "Upload",
  },
  {
    href: "selection",
    label: "Selection",
  },
  {
    href: "training",
    label: "Training",
  },
  {
    href: "prediction",
    label: "Prediction",
  },
  {
    href: "information",
    label: "Additional Information",
  },
];
export const Sidebar = () => (
  <section className="side-nav">
    <Nav className="flex-column">
      {pages.map(({ href, label }) => (
        <Nav.Link
          className={`side-link ${
            window.location.pathname === `/${href}` && "active"
          }`}
          href={`/${href}`}
        >
          {label}
        </Nav.Link>
      ))}
    </Nav>
    <div className="vr"></div>
  </section>
);
