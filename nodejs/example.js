
import { Sophia, Router } from './src/index.js';

/**
 * Callback for vacation-related verbs
 * @param {number} verbPosition - The verb position
 * @param {number} phraseNum - The phrase number
 * @param {Object} phrase - The phrase data
 * @param {Object} output - The full output
 */
async function vacation(verbPosition, phraseNum, phrase, output) {
  for (const noun of phrase.nouns) {
    const token = output.mwe[noun.head];
    console.log(`Looks like we're vacationing in ${token.word}`);
  }
}

async function main() {
  const nlu = new Sophia();
  const router = new Router();

  router.add('verbs/action/travel/depart', vacation);
  await nlu.route(router, 'I want to take off to Thailand and have some fun');
  console.log('Done');
}

main().catch(console.error);



