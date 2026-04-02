import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './Slideshow.module.css';

type Slide = {
  title: string;
  content: string;
  image?: string;
  color?: string;
};

type SlideshowProps = {
  slides: Slide[];
  autoPlay?: boolean;
  interval?: number;
};

export default function Slideshow({ slides, autoPlay = true, interval = 5000 }: SlideshowProps): JSX.Element {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  // Filter slides to only include those with content
  const validSlides = slides.filter(slide => slide.content.trim() !== '');

  // Auto-advance slides
  useEffect(() => {
    if (!autoPlay || isPaused || validSlides.length <= 1) return;

    const slideInterval = setInterval(() => {
      setCurrentIndex((prevIndex) =>
        prevIndex === validSlides.length - 1 ? 0 : prevIndex + 1
      );
    }, interval);

    return () => clearInterval(slideInterval);
  }, [autoPlay, isPaused, interval, validSlides.length]);

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
  };

  const goToPrevious = () => {
    setCurrentIndex(currentIndex === 0 ? validSlides.length - 1 : currentIndex - 1);
  };

  const goToNext = () => {
    setCurrentIndex(currentIndex === validSlides.length - 1 ? 0 : currentIndex + 1);
  };

  if (validSlides.length === 0) {
    return <div className={styles.noSlides}>No slides available</div>;
  }

  return (
    <div
      className={clsx(styles.slideshow, 'slideshow-container')}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      <div className={styles.slides}>
        {validSlides.map((slide, index) => (
          <div
            key={index}
            className={clsx(
              styles.slide,
              index === currentIndex ? styles.active : styles.inactive
            )}
            style={{
              backgroundColor: slide.color || 'rgba(255, 255, 255, 0.9)',
              display: index === currentIndex ? 'block' : 'none'
            }}
          >
            <div className={styles.slideContent}>
              <h2 className={styles.slideTitle}>{slide.title}</h2>
              <div
                className={styles.slideText}
                dangerouslySetInnerHTML={{ __html: slide.content }}
              />
              {slide.image && (
                <div className={styles.slideImage}>
                  <img src={slide.image} alt={slide.title} />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Navigation controls */}
      <div className={styles.navigation}>
        <button
          className={clsx(styles.navButton, styles.prevButton)}
          onClick={goToPrevious}
          aria-label="Previous slide"
        >
          &#10094;
        </button>

        <div className={styles.indicators}>
          {validSlides.map((_, index) => (
            <button
              key={index}
              className={clsx(
                styles.indicator,
                index === currentIndex ? styles.activeIndicator : ''
              )}
              onClick={() => goToSlide(index)}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>

        <button
          className={clsx(styles.navButton, styles.nextButton)}
          onClick={goToNext}
          aria-label="Next slide"
        >
          &#10095;
        </button>
      </div>

      {/* Progress bar */}
      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{
            width: '100%',
            animation: `progress ${interval}ms linear ${isPaused ? 'paused' : 'running'}`
          }}
        />
      </div>
    </div>
  );
}