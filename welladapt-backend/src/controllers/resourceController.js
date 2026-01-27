class ResourceController {
  async getResources(req, res, next) {
    try {
      const resources = {
        general: [
          {
            title: 'University Counseling Services',
            description: 'Free counseling for all students',
            contact: 'counseling@university.lk',
            language: ['si', 'en'],
          },
          {
            title: 'Online Self-Help Resources',
            description: 'Guided exercises and articles',
            url: 'https://example.com/resources',
            language: ['si', 'en'],
          },
        ],
      };

      res.status(200).json({
        success: true,
        data: resources,
      });
    } catch (error) {
      next(error);
    }
  }

  async getCrisisResources(req, res, next) {
    try {
      const crisisResources = {
        helplines: [
          {
            name: 'National Mental Health Helpline',
            number: '1926',
            available: '24/7',
            language: ['si', 'en', 'ta'],
          },
          {
            name: 'Sumithrayo',
            number: '011-2682535',
            available: '24/7',
            language: ['si', 'en'],
          },
        ],
        urgent: {
          message: 'If you\'re in immediate danger, please call 119 or visit the nearest hospital emergency room.',
        },
      };

      res.status(200).json({
        success: true,
        data: crisisResources,
      });
    } catch (error) {
      next(error);
    }
  }

  async getAcademicResources(req, res, next) {
    try {
      const academicResources = {
        exam_stress: [
          {
            title: 'Exam Preparation Guide',
            description: 'Effective study strategies and time management',
            type: 'guide',
          },
          {
            title: 'Relaxation Techniques',
            description: 'Breathing exercises and mindfulness for exam anxiety',
            type: 'exercise',
          },
        ],
      };

      res.status(200).json({
        success: true,
        data: academicResources,
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new ResourceController();