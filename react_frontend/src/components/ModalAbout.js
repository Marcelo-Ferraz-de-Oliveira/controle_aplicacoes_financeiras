import React from "react";
import { Modal } from "react-bootstrap";
// import { useState } from "react";

const ModalAbout = ({ showAbout, setShowAbout }) => {
  // const [showAbout, setShowAbout] = useState(true);

  return (
    <Modal show={showAbout} onHide={() => setShowAbout(false)}>
      <Modal.Header
        closeButton
        className="bg-light text-dark border-0"
      ></Modal.Header>
      <Modal.Body>
        <p>
          Software para ler notas de negociação (corretagem), consolidar a
          posição acionária e calcular o lucro e imposto de renda a pagar.
        </p>
        <p>
          Atualmente suporta notas de negociação das corretoras XP, Clear e
          Genial.
        </p>
      </Modal.Body>
    </Modal>
  );
};

export default ModalAbout;
