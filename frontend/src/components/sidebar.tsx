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
  }
];

export const Sidebar = () => {
  const prefix = process.env.REACT_APP_PREFIX;
  return (
    <section className="side-nav">
      <Nav className="flex-column">
        {pages.map(({ href, label }) => (
          <Nav.Link
            className={`side-link ${
              window.location.pathname === `${prefix}/${href}` && "active"
            }`}
            href={`${prefix}/${href}`}
          >
            {label}
          </Nav.Link>
        ))}
      </Nav>
      <div className="vr"></div>
    </section>
  );
};
