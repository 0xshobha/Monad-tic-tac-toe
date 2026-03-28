// Delhi traffic-themed messages for the game
export const delhiJokes = [
  "Traffic jam ho gaya! 🚧",
  "Signal tod diya! 🚦",
  "Metro le le bhai! 🚇",
  "Horn mat baja, patience rakh! 📯",
  "Carpool karo, pollution kam karo! 🌱",
  "Delhi mein metro le le bhai, better hai! 🚊",
  "Smooth ride mil gaya! ✨",
  "Red light dekh ke ruk ja! 🛑",
  "Green signal, chalo! 🚦",
  "Traffic police aa rahi hai! 👮",
  "Pothole se bach ke! 🕳️",
  "Auto wala meter laga! 🛺",
  "Rickshaw race shuru! 🏁",
  "Delhi ki garmi aur traffic! ☀️",
  "Connaught Place ka chakkar! 🔄",
];

export function getRandomDelhiJoke(): string {
  return delhiJokes[Math.floor(Math.random() * delhiJokes.length)];
}

export const delhiErrorMessages = {
  cellOccupied: "Arre bhai, wahan already gaadi khadi hai! 🚗",
  gameNotFound: "Game ID nahi mila! Check kar le bhai 🔍",
  notYourTurn: "Arre ruk ja, tera turn nahi hai! ⏸️",
  needBadge: "Pehle badge le le, phir khel! 🎫",
  insufficientGas: "MON tokens khatam! Faucet se le le: 💰",
  networkError: "Network slow hai, retry kar! 📡",
};
