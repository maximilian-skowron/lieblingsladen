import React from "react";

import AddToCartButton from "./AddToCartButton";

const AddToCart: React.FC<{
  disabled: boolean;
  onSubmit: () => void;
}> = ({ onSubmit, disabled }) => {
  return (
    <AddToCartButton
      className="product-description__action"
      onClick={() => {
        onSubmit();
      }}
      disabled={disabled}
    >
      In den Warenkorb
    </AddToCartButton>
  );
};

export default AddToCart;
