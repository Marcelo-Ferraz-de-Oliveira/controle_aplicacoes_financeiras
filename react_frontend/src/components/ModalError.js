import React from "react";
import { Modal } from "react-bootstrap";

const ModalError = ({ error, onHide }) => {
  return (
    <Modal show={error !== ""} onHide={onHide}>
      <Modal.Header closeButton className="bg-danger text-light border-0">
        {error}
      </Modal.Header>
    </Modal>
  );
};

export default ModalError;
