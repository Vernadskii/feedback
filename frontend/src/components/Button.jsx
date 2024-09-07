/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable react/prop-types */
/* eslint-disable jsdoc/require-jsdoc */
/* eslint-disable react/button-has-type */

import { cva } from 'class-variance-authority'

const button = cva('rounded-sm px-4 py-2.5 text-base font-semibold', {
  variants: {
    variant: {
      bluePrimary: '',
      blueSecondary: '',
      blueGhost: '',
      monochromePrimary: '',
      monochromeSecondary: '',
      monochromeGhost: '',
      destructive: '',
    },
    fullWidth: {
      true: 'w-full',
    },
    disabled: {
      true: '',
    },
  },
})

function Button({ children, variant, fullWidth, disabled }) {
  return (
    <button className={button({ variant, fullWidth, disabled })}>
      {children}
    </button>
  )
}

export default Button
