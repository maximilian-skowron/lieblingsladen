import React from "react";

const ForgottenPassword: React.FC<{
  onClick: () => void;
}> = ({ onClick }) => (
  <>
    <div className="login__content__password-reminder">
      <p>
        Password vergessen?&nbsp;
        <span className="u-link" onClick={onClick}>
          Hier klicken
        </span>
      </p>
    </div>
  </>
);

export default ForgottenPassword;
