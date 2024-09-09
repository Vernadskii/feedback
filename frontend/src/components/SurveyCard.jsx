function SurveyCard() {
  return (
    <div className="rounded max-w-[274px] rounded-xl px-6 py-5">
      <div className="mb-4">
        <div className="mb-1.5 flex items-center justify-between">
          <p className="text-xs font-semibold">21.07 – 21.08</p>
          <p className="text-xs font-semibold">low</p>
        </div>
        <p className="h-[62px] text-base font-semibold">
          Тест коммуникации по карточке лояльности
        </p>
      </div>
      <div>
        <p className="mb-1 text-xs font-semibold">
          Канал<span className="ml-1.5">Email</span>
        </p>
        <p className="mb-1 text-xs font-semibold">
          Коммуникации<span className="ml-1.5">30</span>
        </p>
        <p className="mb-1 text-xs font-semibold">
          Ответы<span className="ml-1.5">5</span>
        </p>
        <p className="text-xs font-semibold">
          Конверсия<span className="ml-1.5">6%</span>
        </p>
      </div>
    </div>
  )
}

export default SurveyCard
