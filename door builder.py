mkdir door-builder-app; cd door-builder-app
npx create-next-app@latest . --typescript
npm install prisma @prisma/client stripe react-stripe-js @stripe/stripe-js axios
npx prisma init
git init